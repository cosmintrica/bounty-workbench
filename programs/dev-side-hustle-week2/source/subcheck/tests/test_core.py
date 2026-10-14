import unittest

from subcheck.core import Cue, Word, analyze, parse_srt, proposed_srt


class CoreTests(unittest.TestCase):
    def test_multiline_bom_and_comma(self):
        self.assertEqual(parse_srt('\ufeff1\r\n00:00:01,250 --> 00:00:03,500\r\nHello\r\nworld\r\n'),
                         [Cue(1, 1.25, 3.5, 'Hello\nworld')])

    def test_malformed_and_duplicate_cues_rejected(self):
        for text in ['', '1\n00:62:00,000 --> 00:63:00,000\nHi',
                     '1\n00:00:03,000 --> 00:00:02,000\nHi',
                     '1\n00:00:01,000 --> 00:00:02,000\nHi\n\n1\n00:00:03,000 --> 00:00:04,000\nHi']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_srt(text)

    def test_cue_boundaries_do_not_create_text_mismatches(self):
        cues = [Cue(1, 0, 1, '<i>Hello</i> there.'), Cue(2, 1, 2, 'WELCOME back!')]
        words = [Word(0, .4, 'Hello', .95), Word(.4, 1, 'there', .95),
                 Word(1, 1.4, 'welcome', .95), Word(1.4, 2, 'back', .95)]
        self.assertEqual(analyze(cues, words, 2), [])

    def test_timing_and_omission_are_distinct(self):
        cues = [Cue(1, 2, 4, 'Welcome back.')]
        words = [Word(0, .5, 'Welcome', .95), Word(.5, 1, 'back.', .95),
                 Word(1.1, 1.5, 'Please', .95), Word(1.5, 2, 'subscribe.', .95)]
        issues = analyze(cues, words, 5)
        self.assertEqual({i['kind'] for i in issues}, {'timing_difference', 'uncovered_speech'})
        self.assertTrue(all(i['severity'] == 'review' for i in issues))

    def test_wrong_word_is_not_declared_confirmed_error(self):
        issues = analyze([Cue(1, 0, 2, 'Send the blue bag')],
                         [Word(0, .4, 'Send', .9), Word(.4, .6, 'the', .9),
                          Word(.6, 1.3, 'red', .9), Word(1.3, 2, 'bag', .9)], 2)
        differences = [i for i in issues if i['kind'] == 'text_difference']
        self.assertEqual(len(differences), 1)
        self.assertEqual(differences[0]['observed'], 'red')
        self.assertEqual(differences[0]['severity'], 'review')

    def test_repeated_words_align_without_omission(self):
        words = [Word(i, i + 1, w, .95) for i, w in enumerate(['go', 'go', 'stop'])]
        self.assertEqual(analyze([Cue(1, 0, 3, 'go go stop')], words, 3), [])

    def test_single_missing_negation_requires_review(self):
        words = [Word(0, .4, 'Do', .95), Word(.4, .8, 'not', .95), Word(.8, 2, 'proceed', .95)]
        issues = analyze([Cue(1, 0, 2, 'Do proceed.')], words, 2)
        self.assertEqual([i['observed'] for i in issues if i['kind'] == 'uncovered_speech'], ['not'])

    def test_identical_cues_are_reported_as_ambiguous(self):
        cues = [Cue(1, 0, 1, 'Go now'), Cue(2, 10, 11, 'Go now')]
        words = [Word(10, 10.5, 'Go', .95), Word(10.5, 11, 'now', .95)]
        issues = analyze(cues, words, 12)
        self.assertEqual([i['kind'] for i in issues], ['ambiguous_alignment', 'ambiguous_alignment'])

    def test_cross_cue_deletion_quotes_only_unmatched_fragments(self):
        cues = [Cue(1, 0, 1, 'alpha beta'), Cue(2, 1, 2, 'gamma delta')]
        words = [Word(0, .5, 'alpha', .95), Word(1.5, 2, 'delta', .95)]
        diffs = [i for i in analyze(cues, words, 2) if i['kind'] == 'text_difference']
        self.assertEqual([i['expected'] for i in diffs], ['beta', 'gamma'])

    def test_cross_cue_replacement_is_one_shared_span(self):
        cues = [Cue(1, 0, 1, 'alpha beta'), Cue(2, 1, 2, 'gamma delta')]
        words = [Word(0, .5, 'alpha', .95), Word(.5, 1.5, 'something', .95), Word(1.5, 2, 'delta', .95)]
        diffs = [i for i in analyze(cues, words, 2) if i['kind'] == 'text_difference']
        self.assertEqual(len(diffs), 1)
        self.assertIsNone(diffs[0]['cue_id'])
        self.assertEqual(diffs[0]['observed'], 'something')

    def test_decreasing_word_ends_are_rejected(self):
        with self.assertRaises(ValueError):
            analyze([], [Word(0, 1, 'Hello', .9), Word(.5, .7, 'there', .9)], 2)

    def test_overlap_past_end_and_reading_speed(self):
        cues = [Cue(1, 0, 2, 'One'), Cue(2, 1, 3, 'A' * 60)]
        kinds = {i['kind'] for i in analyze(cues, [], 2.5)}
        self.assertTrue({'overlap', 'past_audio_end', 'reading_speed', 'no_speech'} <= kinds)

    def test_invalid_recognition_times_rejected(self):
        with self.assertRaises(ValueError):
            analyze([], [Word(float('nan'), 1, 'hello', .9)], 3)

    def test_asr_draft_roundtrips_and_preserves_words(self):
        words = [Word(i / 2, i / 2 + .4, w, .95)
                 for i, w in enumerate('A small local tool makes subtitle review easier for busy freelance editors'.split())]
        draft = parse_srt(proposed_srt(words))
        self.assertEqual(' '.join(c.text.replace('\n', ' ') for c in draft),
                         ' '.join(w.text for w in words))
        self.assertTrue(all(c.end > c.start for c in draft))


if __name__ == '__main__':
    unittest.main()
