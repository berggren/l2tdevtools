#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the download helper object implementations."""

import os
import shutil
import tempfile
import unittest

from l2tdevtools import download_helper


class TempDirectory(object):
  """A self cleaning temporary directory."""

  def __init__(self):
    """Initializes the temporary directory."""
    super(TempDirectory, self).__init__()
    self.name = u''

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self.name = tempfile.mkdtemp()
    return self.name

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Make this work with the 'with' statement."""
    shutil.rmtree(self.name, True)


class DownloadHelperTest(unittest.TestCase):
  """Tests for the download helper."""

  _FILENAME = u'LICENSE'

  def setUp(self):
    """Sets up a test case."""
    self._download_url = (
        u'https://raw.githubusercontent.com/log2timeline/devtools/master/'
        u'{0:s}').format(self._FILENAME)

  def testDownloadPageContent(self):
    """Tests the DownloadPageContent functions."""
    download_helper_object = download_helper.DownloadHelper()

    page_content = download_helper_object.DownloadPageContent(
        self._download_url)

    expected_page_content = b''
    with open(self._FILENAME, 'rb') as file_object:
      expected_page_content = file_object.read()

    self.assertEqual(page_content, expected_page_content)

  def testDownloadFile(self):
    """Tests the DownloadFile functions."""
    download_helper_object = download_helper.DownloadHelper()

    current_working_directory = os.getcwd()

    page_content = b''
    with TempDirectory() as temporary_directory:
      os.chdir(temporary_directory)
      filename = download_helper_object.DownloadFile(self._download_url)

      with open(filename, 'rb') as file_object:
        page_content = file_object.read()

    os.chdir(current_working_directory)

    expected_page_content = b''
    with open(self._FILENAME, 'rb') as file_object:
      expected_page_content = file_object.read()

    self.assertEqual(page_content, expected_page_content)


class GoogleCodeWikiDownloadHelperTest(unittest.TestCase):
  """Tests for the Google code wiki download helper."""

  _PROJECT_NAME = u'binplist'
  _PROJECT_VERSION = u'0.1.4'

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.GoogleCodeWikiDownloadHelper()

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.GoogleCodeWikiDownloadHelper()

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'https://{0:s}.googlecode.com/files/{0:s}-{1:s}.tar.gz').format(
            self._PROJECT_NAME, self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.GoogleCodeWikiDownloadHelper()

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'com.google.code.p.{0:s}'.format(
        self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


class LibyalGoogleDriveDownloadHelperTest(unittest.TestCase):
  """Tests for the libyal Google drive download helper."""

  _PROJECT_NAME = u'libewf'
  _PROJECT_VERSION = 20140608
  _DRIVE_URL = (
      u'https://googledrive.com/host/0B3fBvzttpiiSMTdoaVExWWNsRjg')

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.LibyalGoogleDriveDownloadHelper(
        self._DRIVE_URL)

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.LibyalGoogleDriveDownloadHelper(
        self._DRIVE_URL)

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'{0:s}/{1:s}-{2:d}.tar.gz').format(
            self._DRIVE_URL, self._PROJECT_NAME, self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.LibyalGoogleDriveDownloadHelper(
        self._DRIVE_URL)

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'com.github.libyal.{0:s}'.format(
        self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


class DocoptGithubReleasesDownloadHelperTest(unittest.TestCase):
  """Tests for the docopt github releases download helper."""

  _PROJECT_ORGANIZATION = u'docopt'
  _PROJECT_NAME = u'docopt'
  _PROJECT_VERSION = u'0.6.2'

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'docopt')

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'docopt')

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'https://github.com/{0:s}/{1:s}/archive/{2:s}.tar.gz').format(
            self._PROJECT_ORGANIZATION, self._PROJECT_NAME,
            self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'docopt')

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'com.github.{0:s}.{1:s}'.format(
        self._PROJECT_ORGANIZATION, self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


class LibyalGithubReleasesDownloadHelperTest(unittest.TestCase):
  """Tests for the libyal github releases download helper."""

  _PROJECT_ORGANIZATION = u'libyal'
  _PROJECT_NAME = u'libevt'
  _PROJECT_STATUS = u'alpha'
  _PROJECT_VERSION = u'20150706'

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'libyal')

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'libyal')

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'https://github.com/{0:s}/{1:s}/releases/download/{3:s}/'
        u'{1:s}-{2:s}-{3:s}.tar.gz').format(
            self._PROJECT_ORGANIZATION, self._PROJECT_NAME,
            self._PROJECT_STATUS, self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'libyal')

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'com.github.{0:s}.{1:s}'.format(
        self._PROJECT_ORGANIZATION, self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


class Log2TimelineGithubReleasesDownloadHelperTest(unittest.TestCase):
  """Tests for the log2timeline github releases download helper."""

  _PROJECT_ORGANIZATION = u'log2timeline'
  _PROJECT_NAME = u'dfvfs'
  _PROJECT_VERSION = u'20150708'

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'log2timeline')

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'log2timeline')

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'https://github.com/{0:s}/{1:s}/releases/download/{2:s}/'
        u'{1:s}-{2:s}.tar.gz').format(
            self._PROJECT_ORGANIZATION, self._PROJECT_NAME,
            self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.GithubReleasesDownloadHelper(
        u'log2timeline')

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'com.github.{0:s}.{1:s}'.format(
        self._PROJECT_ORGANIZATION, self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


class PyPiDownloadHelperTest(unittest.TestCase):
  """Tests for the PyPi download helper."""

  _PROJECT_NAME = u'construct'
  _PROJECT_VERSION = u'2.5.2'

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.PyPiDownloadHelper()

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.PyPiDownloadHelper()

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'https://pypi.python.org/packages/source/{0:s}/{1:s}/'
        u'{1:s}-{2:s}.tar.gz').format(
            self._PROJECT_NAME[0], self._PROJECT_NAME, self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.PyPiDownloadHelper()

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'org.python.pypi.{0:s}'.format(
        self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


class SourceForgeDownloadHelperTest(unittest.TestCase):
  """Tests for the Source Forge download helper."""

  _PROJECT_NAME = u'pyparsing'
  _PROJECT_VERSION = u'2.0.3'

  def testGetLatestVersion(self):
    """Tests the GetLatestVersion functions."""
    download_helper_object = download_helper.SourceForgeDownloadHelper()

    latest_version = download_helper_object.GetLatestVersion(self._PROJECT_NAME)

    self.assertEqual(latest_version, self._PROJECT_VERSION)

  def testGetDownloadUrl(self):
    """Tests the GetDownloadUrl functions."""
    download_helper_object = download_helper.SourceForgeDownloadHelper()

    download_url = download_helper_object.GetDownloadUrl(
        self._PROJECT_NAME, self._PROJECT_VERSION)

    expected_download_url = (
        u'http://downloads.sourceforge.net/project/{0:s}/{0:s}/{0:s}-{1:s}'
        u'/{0:s}-{1:s}.tar.gz').format(
            self._PROJECT_NAME, self._PROJECT_VERSION)

    self.assertEqual(download_url, expected_download_url)

  def testGetProjectIdentifier(self):
    """Tests the GetProjectIdentifier functions."""
    download_helper_object = download_helper.SourceForgeDownloadHelper()

    project_identifier = download_helper_object.GetProjectIdentifier(
        self._PROJECT_NAME)

    expected_project_identifier = u'net.sourceforge.projects.{0:s}'.format(
        self._PROJECT_NAME)

    self.assertEqual(project_identifier, expected_project_identifier)


if __name__ == '__main__':
  unittest.main()
