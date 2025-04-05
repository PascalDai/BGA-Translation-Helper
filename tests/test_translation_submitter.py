import unittest
from src.submitter.translation_submitter import TranslationSubmitter

class TestTranslationSubmitter(unittest.TestCase):
    def setUp(self):
        self.submitter = TranslationSubmitter()

    def test_login(self):
        """测试登录功能"""
        self.assertTrue(self.submitter.login())

    def test_load_translations(self):
        """测试加载翻译表"""
        translations = self.submitter.load_translations()
        self.assertIsNotNone(translations)
        self.assertIsInstance(translations, dict)

    def test_submit_translation(self):
        """测试提交翻译"""
        result = self.submitter.submit_translation("test", "测试")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main() 