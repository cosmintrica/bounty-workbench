from argparse import Namespace
from pathlib import Path
import tempfile
import unittest

from subcheck.cli import audit, load_model_metadata, markdown_report
from subcheck.core import analyze


class InputTests(unittest.TestCase):
    def test_existing_report_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            audio, captions, out = base / 'audio.wav', base / 'captions.srt', base / 'review'
            audio.touch()
            captions.touch()
            out.mkdir()
            original = out / 'report.md'
            original.write_text('my reviewed work')
            with self.assertRaisesRegex(ValueError, 'must be empty'):
                audit(Namespace(audio=audio, captions=captions, output=out))
            self.assertEqual(original.read_text(), 'my reviewed work')

    def test_missing_local_model_is_clear(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'Missing local model file'):
                load_model_metadata(Path(folder))

    def test_nonnumeric_thresholds_rejected(self):
        for value in [float('nan'), float('inf'), -1]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze([], [], 1, max_cps=value)

    def test_no_findings_report_does_not_claim_accuracy(self):
        report = dict(summary=dict(cues=1, words=2, issues=0), duration_seconds=2,
                      elapsed_seconds=.2, issues=[], limitations=[],
                      model=dict(name='test', revision='test'))
        text = markdown_report(report)
        self.assertIn('not a guarantee of accuracy', text)
        self.assertIn('Human review required', text)


if __name__ == '__main__':
    unittest.main()
