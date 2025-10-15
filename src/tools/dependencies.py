
"""This module contains the dependency analysis tools for the MCP server."""

import os
import json
import logging
import requests
from .utils import is_safe_path

logger = logging.getLogger(__name__)

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
