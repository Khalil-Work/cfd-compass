from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("validation", Path(__file__).parents[1] / "tools/validate.py")
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)


class CatalogueChecks(unittest.TestCase):
    def setUp(self):
        self.entries = [{"name":"Example", "repo":"Owner/Project", "category":"flow", "summary":"A teaching flow solver.", "best_for":"Learning", "tags":["flow", "education"], "docs_url":"https://example.org/docs", "source_urls":["https://github.com/Owner/Project"], "caveat":"", "maturity":"research"}]
        self.categories = [{"id":"flow"}]
        self.metadata = {"repositories":{"owner/project":{"full_name":"Owner/Project", "html_url":"https://github.com/Owner/Project", "private":False}}}

    def test_valid(self):
        self.assertEqual(validation.validate(self.entries,self.categories,self.metadata),[])

    def test_case_insensitive_duplicate(self):
        self.entries.append({**self.entries[0],"repo":"owner/project"})
        self.assertTrue(any("duplicate" in e for e in validation.validate(self.entries,self.categories)))

    def test_unknown_category_and_missing_source(self):
        self.entries[0]["category"]="missing"
        self.entries[0]["source_urls"]=[]
        errors=validation.validate(self.entries,self.categories)
        self.assertTrue(any("unknown category" in e for e in errors))
        self.assertTrue(any("no primary source" in e for e in errors))

    def test_malicious_url_is_rejected(self):
        self.entries[0]["docs_url"]="javascript:alert(1)"
        self.assertTrue(any("invalid source URL" in e for e in validation.validate(self.entries,self.categories)))

    def test_stale_canonical_name_is_rejected(self):
        self.metadata["repositories"]["owner/project"]["full_name"]="NewOwner/Project"
        self.assertTrue(any("canonical name mismatch" in e for e in validation.validate(self.entries,self.categories,self.metadata)))

    def test_private_and_missing_metadata_are_rejected(self):
        self.metadata["repositories"]["owner/project"]["private"]=True
        self.assertTrue(any("private" in e for e in validation.validate(self.entries,self.categories,self.metadata)))
        self.assertTrue(any("no checked API" in e for e in validation.validate(self.entries,self.categories,{"repositories":{}})))

    def test_malformed_contribution_types_report_errors(self):
        self.entries[0].update(summary=None, source_urls=None, tags=["flow", "FLOW"], caveat=[])
        errors=validation.validate(self.entries,self.categories)
        self.assertTrue(any("empty summary" in e for e in errors))
        self.assertTrue(any("duplicate tags" in e for e in errors))
        self.assertTrue(any("source_urls must" in e for e in errors))

    def test_executable_metadata_url_is_rejected(self):
        self.metadata["repositories"]["owner/project"]["html_url"]="javascript:alert(1)"
        self.assertTrue(any("canonical HTTPS" in e for e in validation.validate(self.entries,self.categories,self.metadata)))

    def test_external_executable_url_is_rejected(self):
        entry={'name':'External','url':'javascript:alert(1)','category':'flow','summary':'Example','kind':'reference','source_urls':['https://example.org'],'access_note':'Inspect terms'}
        self.assertTrue(any('invalid external URL' in e for e in validation.validate_external([entry],self.categories)))


if __name__ == "__main__":
    unittest.main()
