"""This module implements a Model Context Protocol (MCP) server for Gemini Agent."""
import json
import logging
import requests
import os
from mcp_instance import mcp
from utils import is_safe_path

logging.basicConfig(level=logging.INFO,
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import subprocess

logger = logging.getLogger(__name__)

def call_gemini_impl(prompt: str, system_instruction: str = '') -> dict:
	"""Implementation of the call_gemini tool."""
	logger.info("Executing call_gemini with prompt: '%s...'")
	full_prompt = f"{system_instruction}\n\n{prompt}"
	try:
		result = subprocess.run(
			['gemini', full_prompt], capture_output=True, text=True, check=True, encoding='utf-8')
		logger.info("call_gemini executed successfully.")
		logger.info(result)
		return {"response": result.stdout}
	except FileNotFoundError as exc:
		logger.error("'gemini' command not found.")
		raise ValueError(
			"'gemini' command not found. Make sure the Gemini CLI is installed and in your PATH."
		) from exc
	except subprocess.CalledProcessError as exc:
		logger.error("Error calling Gemini CLI: %s", exc.stderr)
		raise RuntimeError(f"Error calling Gemini CLI: {exc.stderr}") from exc
	except Exception as exc:
		logger.error("An unexpected error occurred in call_gemini: %s", exc)
		raise RuntimeError(f"An unexpected error occurred: {exc}") from exc

@mcp.tool
def call_gemini(prompt: str, system_instruction: str = '') -> dict:
	"""Calls the Gemini CLI with a given prompt and context."""
	return call_gemini_impl(prompt, system_instruction)


@mcp.tool
def create_github_issue(repo_owner: str, repo_name: str, title: str, body: str = '') -> dict:
	"""Creates a new issue in a GitHub repository."""
	logger.info("Executing create_github_issue for repo: %s/%s", repo_owner, repo_name)
	github_token = os.environ.get("GITHUB_TOKEN")
	if not github_token:
		logger.error("GITHUB_TOKEN environment variable not set.")
		raise ValueError("GITHUB_TOKEN environment variable not set.")

	url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
	headers = {
		"Authorization": f"token {github_token}",
		"Accept": "application/vnd.github.v3+json"
	}
	payload = {"title": title, "body": body}

	try:
		response = requests.post(url, headers=headers, json=payload, timeout=10)
		response.raise_for_status()
		logger.info("GitHub issue created successfully: %s", response.json().get('html_url'))
		return {"issue_url": response.json().get('html_url')}
	except requests.exceptions.RequestException as exc:
		logger.error("Error creating GitHub issue: %s", exc)
		raise RuntimeError(f"Error creating GitHub issue: {exc}") from exc

# pylint: disable=too-many-arguments
@mcp.tool
def create_github_pr(
	repo_owner: str, repo_name: str, title: str, head: str, base: str, body: str = ''
) -> dict:
	"""Creates a new pull request in a GitHub repository."""
	logger.info("Executing create_github_pr for repo: %s/%s", repo_owner, repo_name)
	github_token = os.environ.get("GITHUB_TOKEN")
	if not github_token:
		logger.error("GITHUB_TOKEN environment variable not set.")
		raise ValueError("GITHUB_TOKEN environment variable not set.")

	url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
	headers = {
		"Authorization": f"token {github_token}",
		"Accept": "application/vnd.github.v3+json"
	}
	payload = {"title": title, "body": body, "head": head, "base": base}

	try:
		response = requests.post(url, headers=headers, json=payload, timeout=10)
		response.raise_for_status()
		logger.info(
			"GitHub pull request created successfully: %s", response.json().get('html_url'))
		return {"pr_url": response.json().get('html_url')}
	except requests.exceptions.RequestException as exc:
		logger.error("Error creating GitHub pull request: %s", exc)
		raise RuntimeError(f"Error creating GitHub pull request: {exc}") from exc

logger = logging.getLogger(__name__)

@mcp.tool
def summarize_docs(files: list) -> dict:
	"""Summarizes the content of a list of documentation files."""
	logger.info("Executing summarize_docs for files: %s", files)
	all_docs_content = ""
	for file_path in files:
		if not is_safe_path(file_path):
			logger.warning("Attempted to access unsafe path: %s", file_path)
			raise ValueError(f"Access to path '{file_path}' is not allowed.")
		try:
			with open(file_path, 'r', encoding='utf-8') as file:
				all_docs_content += file.read() + "\n\n"
		except FileNotFoundError as exc:
			logger.error("File not found: %s", file_path)
			raise FileNotFoundError(f"File not found: {file_path}") from exc
		except Exception as exc:
			logger.error("Error reading file %s: %s", file_path, exc)
			raise IOError(f"Error reading file {file_path}: {exc}") from exc

	if not all_docs_content:
		logger.warning("No content found in the provided files for summarize_docs.")
		raise ValueError("No content found in the provided files.")

	prompt = f"Please summarize the following documentation:\n\n{all_docs_content}"
	return call_gemini_impl(prompt)

@mcp.tool
def generate_docstrings(file_path: str) -> dict:
	"""Generates docstrings for functions or classes in a given file."""

@mcp.tool
def analyze_dependencies(file_path: str) -> dict:
	"""Analyzes a dependency file and provides a summary of each dependency."""
	logger.info("Executing analyze_dependencies for file: %s", file_path)
	if not is_safe_path(file_path):
		logger.warning("Attempted to access unsafe path: %s", file_path)
		raise ValueError(f"Access to path '{file_path}' is not allowed.")

	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()
	except FileNotFoundError as exc:
		logger.error("File not found: %s", file_path)
		raise FileNotFoundError(f"File not found: {file_path}") from exc
	except Exception as exc:
		logger.error("Error reading file %s: %s", file_path, exc)
		raise IOError(f"Error reading file {file_path}: {exc}") from exc

	report = {}
	if os.path.basename(file_path) == 'requirements.txt':
		packages = [line.strip() for line in content.splitlines()
					if line.strip() and not line.startswith('#')]
		for package in packages:
			package_name = package.split('==')[0].split('>=')[0].split('<=')[0]
			package_name = package_name.split('<')[0].split('>')[0]
			try:
				response = requests.get(
					f"https://pypi.org/pypi/{package_name}/json", timeout=10)
				response.raise_for_status()
				package_info = response.json()['info']
				report[package_name] = {
					"summary": package_info.get('summary'),
					"latest_version": package_info.get('version'),
					"license": package_info.get('license')
				}
			except requests.exceptions.RequestException as exc:
				logger.warning(
					"Could not fetch details for PyPI package %s: %s", package_name, exc)
				report[package_name] = {"error": f"Could not fetch details: {exc}"}

	elif os.path.basename(file_path) == 'package.json':
		try:
			data = json.loads(content)
			dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
			for package_name in dependencies.keys():
				try:
					response = requests.get(
						f"https://registry.npmjs.org/{package_name}", timeout=10)
					response.raise_for_status()
					package_info = response.json()
					report[package_name] = {
						"summary": package_info.get('description'),
						"latest_version": package_info.get('dist-tags', {}).get('latest'),
						"license": package_info.get('license')
					}
				except requests.exceptions.RequestException as exc:
					logger.warning(
						"Could not fetch details for npm package %s: %s", package_name, exc)
					report[package_name] = {"error": f"Could not fetch details: {exc}"}
		except json.JSONDecodeError as exc:
			logger.error("Invalid package.json file.")
			raise ValueError("Invalid package.json file.") from exc
	else:
		logger.warning("Unsupported file type for analyze_dependencies: %s", file_path)
		raise ValueError(
			"Unsupported file type. Supported files are 'requirements.txt' and 'package.json'."
		)

	logger.info("analyze_dependencies for %s executed successfully.", file_path)
	return {"dependency_report": report}

	@mcp.tool
	def lint_code(file_path: str, language: str) -> dict:
		"""Lints a Python or JavaScript file and returns a report of issues."""
		logger.info("Executing lint_code for file: %s (%s)", file_path, language)
		if not is_safe_path(file_path):
			logger.warning("Attempted to access unsafe path: %s", file_path)
			raise ValueError(f"Access to path '{file_path}' is not allowed.")

		if language == "python":
			linter_command = ["pylint", file_path]
		elif language == "javascript":
			linter_command = ["eslint", file_path]
		else:
			logger.warning("Unsupported language for lint_code: %s", language)
			raise ValueError(
				f"Unsupported language: {language}. Supported languages are 'python' and 'javascript'."
			)

		try:
			result = subprocess.run(
				linter_command, capture_output=True, text=True, check=False, encoding='utf-8')
			logger.info("lint_code for %s executed successfully.", file_path)
			return {"linting_report": result.stdout}
		except FileNotFoundError as exc:
			logger.error("'%s' command not found.", linter_command[0])
			raise ValueError(
				f"'{linter_command[0]}' command not found. "
				f"Make sure the linter is installed and in your PATH."
			) from exc
		except Exception as exc:
			logger.error("An unexpected error occurred in lint_code: %s", exc)
			raise RuntimeError(f"An unexpected error occurred: {exc}") from exc

	@mcp.tool
	def generate_unit_tests(file_path: str, item_name: str) -> dict:
		"""Generates unit tests for a given function or class in a file."""
		logger.info(
			"Executing generate_unit_tests for item '%s' in file: %s", item_name, file_path)
		if not is_safe_path(file_path):
			logger.warning("Attempted to access unsafe path: %s", file_path)
			raise ValueError(f"Access to path '{file_path}' is not allowed.")

		try:
			with open(file_path, 'r', encoding='utf-8') as file:
				file_content = file.read()
		except FileNotFoundError as exc:
			logger.error("File not found: %s", file_path)
			raise FileNotFoundError(f"File not found: {file_path}") from exc
		except Exception as exc:
			logger.error("Error reading file %s: %s", file_path, exc)
			raise IOError(f"Error reading file {file_path}: {exc}") from exc

		prompt = (
			f"Generate unit tests for the function or class '{item_name}' in the following code:"
			f"\n\n```\n{file_content}\n```"
		)
		return call_gemini_impl(prompt)

if __name__ == "__main__":
	mcp.run(transport="http", host="0.0.0.0", port=8000)
