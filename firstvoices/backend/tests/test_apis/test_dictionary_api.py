import json

import factory
import pytest
from factory.django import DjangoModelFactory

from backend.models import dictionary
from backend.models.constants import Role, Visibility
from backend.tests import factories

from .base_api_test import BaseSiteControlledContentApiTest


class AcknowledgementFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.Acknowledgement


class AlternateSpellingFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.AlternateSpelling


class NoteFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.Note


class PronunciationFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.Pronunciation


class TranslationFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.Translation


class DictionaryEntryLinkFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.DictionaryEntryLink

    from_dictionary_entry = factory.SubFactory(factories.DictionaryEntryFactory)
    to_dictionary_entry = factory.SubFactory(factories.DictionaryEntryFactory)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.Category

    title = factory.Sequence(lambda n: "Category %03d" % n)
    created_by = factory.SubFactory(factories.UserFactory)
    last_modified_by = factory.SubFactory(factories.UserFactory)


class DictionaryEntryCategoryFactory(DjangoModelFactory):
    class Meta:
        model = dictionary.DictionaryEntryCategory

    dictionary_entry = factory.SubFactory(factories.DictionaryEntryFactory)
    category = factory.SubFactory(CategoryFactory)


class TestDictionaryEndpoint(BaseSiteControlledContentApiTest):
    """
    End-to-end tests that the dictionary endpoints have the expected behaviour.
    """

    API_LIST_VIEW = "api:dictionaryentry-list"
    API_DETAIL_VIEW = "api:dictionaryentry-detail"

    def get_expected_response(self, entry, site):
        return {
            "url": f"http://testserver{self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))}",
            "id": str(entry.id),
            "title": entry.title,
            "type": "WORD",
            "customOrder": entry.custom_order,
            "visibility": "Public",
            "categories": [],
            "excludeFromGames": False,
            "excludeFromKids": False,
            "acknowledgements": [],
            "alternateSpellings": [],
            "notes": [],
            "translations": [],
            "pronunciations": [],
            "site": {
                "title": site.title,
                "slug": site.slug,
                "url": f"http://testserver/api/1.0/sites/{site.slug}/",
                "language": None,
                "visibility": "Public",
            },
            "created": entry.created.astimezone().isoformat(),
            "lastModified": entry.last_modified.astimezone().isoformat(),
        }

    @pytest.mark.django_db
    def test_list_full(self):
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        site = factories.SiteFactory(visibility=Visibility.PUBLIC)
        entry = factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.PUBLIC
        )
        factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.MEMBERS
        )
        factories.DictionaryEntryFactory.create(site=site, visibility=Visibility.TEAM)

        response = self.client.get(self.get_list_endpoint(site_slug=site.slug))

        assert response.status_code == 200

        response_data = json.loads(response.content)
        assert response_data["count"] == 1
        assert len(response_data["results"]) == 1

        assert response_data["results"][0] == self.get_expected_response(entry, site)

    @pytest.mark.django_db
    def test_list_permissions(self):
        # create some visible words and some invisible words
        site = factories.SiteFactory(visibility=Visibility.PUBLIC)
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        factories.DictionaryEntryFactory.create(site=site, visibility=Visibility.PUBLIC)
        factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.MEMBERS
        )
        factories.DictionaryEntryFactory.create(site=site, visibility=Visibility.TEAM)

        response = self.client.get(self.get_list_endpoint(site.slug))

        assert response.status_code == 200
        response_data = json.loads(response.content)

        assert response_data["count"] == 1, "did not filter out blocked sites"
        assert len(response_data["results"]) == 1, "did not include available site"

    @pytest.mark.django_db
    def test_detail(self):
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        site = factories.SiteFactory(visibility=Visibility.PUBLIC)
        entry = factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.PUBLIC
        )
        factories.DictionaryEntryFactory.create(site=site, visibility=Visibility.PUBLIC)

        response = self.client.get(
            self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))
        )

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data == self.get_expected_response(entry, site)

    @pytest.mark.parametrize(
        "field",
        [
            {"factory": AlternateSpellingFactory, "name": "alternateSpellings"},
            {"factory": AcknowledgementFactory, "name": "acknowledgements"},
            {"factory": NoteFactory, "name": "notes"},
            {"factory": PronunciationFactory, "name": "pronunciations"},
        ],
        ids=["alternateSpellings", "acknowledgements", "notes", "pronunciations"],
    )
    @pytest.mark.django_db
    def test_detail_fields(self, field):
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        site = factories.SiteFactory(visibility=Visibility.PUBLIC)
        entry = factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.PUBLIC
        )
        factories.DictionaryEntryFactory.create(site=site, visibility=Visibility.PUBLIC)

        text = "bon mots"
        field["factory"].create(dictionary_entry=entry, text=text)

        response = self.client.get(
            self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))
        )

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data[field["name"]] == [{"text": f"{text}"}]

    @pytest.mark.django_db
    def test_detail_translations(self):
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        site = factories.SiteFactory(visibility=Visibility.PUBLIC)
        entry = factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.PUBLIC
        )
        factories.DictionaryEntryFactory.create(site=site, visibility=Visibility.PUBLIC)

        text = "bon mots"
        TranslationFactory.create(dictionary_entry=entry, text=text)

        response = self.client.get(
            self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))
        )

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data["translations"] == [
            {
                "text": f"{text}",
                "language": "EN",
                "partOfSpeech": None,
            }
        ]

    @pytest.mark.django_db
    def test_detail_categories(self):
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        site = factories.SiteFactory(visibility=Visibility.PUBLIC)
        entry = factories.DictionaryEntryFactory.create(
            site=site, visibility=Visibility.PUBLIC
        )

        category1 = CategoryFactory(site=site, title="test category A")
        category2 = CategoryFactory(site=site, title="test category B")
        CategoryFactory(site=site)

        DictionaryEntryCategoryFactory(category=category1, dictionary_entry=entry)
        DictionaryEntryCategoryFactory(category=category2, dictionary_entry=entry)

        response = self.client.get(
            self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))
        )

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data["categories"] == [
            {
                "title": f"{category1.title}",
                "id": str(category1.id),
                "url": f"http://testserver/api/1.0/sites/{site.slug}/categories/{str(category1.id)}/",
            },
            {
                "title": f"{category2.title}",
                "id": str(category2.id),
                "url": f"http://testserver/api/1.0/sites/{site.slug}/categories/{str(category2.id)}/",
            },
        ]

    @pytest.mark.django_db
    def test_detail_team_access(self):
        site = factories.SiteFactory.create(visibility=Visibility.PUBLIC)
        user = factories.get_non_member_user()
        factories.MembershipFactory.create(user=user, site=site, role=Role.ASSISTANT)
        self.client.force_authenticate(user=user)

        entry = factories.DictionaryEntryFactory.create(
            visibility=Visibility.TEAM, site=site
        )

        response = self.client.get(
            self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))
        )

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data["id"] == str(entry.id)

    @pytest.mark.django_db
    def test_detail_403_entry_not_visible(self):
        site = factories.SiteFactory.create(visibility=Visibility.PUBLIC)
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        entry = factories.DictionaryEntryFactory.create(
            visibility=Visibility.TEAM, site=site
        )

        response = self.client.get(
            self.get_detail_endpoint(site_slug=site.slug, key=str(entry.id))
        )

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_detail_404_unknown_site(self):
        user = factories.get_non_member_user()
        self.client.force_authenticate(user=user)

        entry = factories.DictionaryEntryFactory.create(visibility=Visibility.PUBLIC)

        response = self.client.get(
            self.get_detail_endpoint(site_slug="fake-site", key=str(entry.id))
        )

        assert response.status_code == 404
