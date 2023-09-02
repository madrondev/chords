from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory
from . import factories


class SongAdminTest(TestCase):
    def setUp(self):
        UserFactory(username='admin')
        self.assertTrue(self.client.login(username='admin', password='pass'))
        self.list = reverse('admin:chords_song_changelist')

    def test_list(self):
        with self.assertNumQueries(6):
            response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)
        for _ in range(5):
            song = factories.SongFactory()
        with self.assertNumQueries(6):
            response = self.client.get(self.list)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:chords_song_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        obj = factories.SongFactory()
        url = reverse('admin:chords_song_change', args=(obj.pk,))
        with self.assertNumQueries(5):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        with self.assertNumQueries(5):
            response = self.client.get(url)

    def test_delete(self):
        obj = factories.SongFactory()
        url = reverse('admin:chords_song_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_source(self):
        obj = factories.SongFactory(title='Let it be', artist='The Beatles', key='C', chords='{sov}\nWhen I [C]find myself in [G]times of trouble\n{eov}')
        url = reverse('admin:chords_song_source', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/plain')
        self.assertEqual(response.headers['Content-Disposition'], 'attachment; filename="the-beatles-let-it-be.cho"')
        lines = response.content.splitlines()
        self.assertEqual(lines[0], b'{title: Let it be}')

    def test_pdf_chords(self):
        obj = factories.SongFactory(title='Amazing grace')
        url = reverse('admin:chords_song_pdf_chords', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/pdf')
        self.assertEqual(response.headers['Content-Disposition'], 'attachment; filename="amazing-grace-chords.pdf"')
        self.assertGreater(len(response.content), 1000)
