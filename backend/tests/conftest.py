import os

# Settings are read when app.main is imported, so the test environment must be
# in place before any test module imports the app. Real environment variables
# take priority over backend/.env, which keeps tests independent of a
# developer's local file.
os.environ["APP_NAME"] = "ai-researcher-test"
os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LLM_API_KEY"] = "test-key"
