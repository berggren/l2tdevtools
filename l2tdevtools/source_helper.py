# -*- coding: utf-8 -*-
"""Source helper object implementations."""

import abc
import glob
import logging
import os
import re
import shutil
import tarfile


class SourceHelper(object):
  """Base class that helps in managing the source code."""

  def __init__(self, project_name):
    """Initializes the source helper.

    Args:
      project_name: the name of the project.
    """
    super(SourceHelper, self).__init__()
    self.project_name = project_name

  @abc.abstractmethod
  def Create(self):
    """Creates the source directory.

    Returns:
      The name of the source directory if successful or None on error.
    """

  @abc.abstractmethod
  def GetProjectIdentifier(self):
    """Retrieves the project identifier for a given project name.

    Returns:
      The project identifier or None on error.
    """


class SourcePackageHelper(SourceHelper):
  """Class that manages the source code from a source package."""

  ENCODING = 'utf-8'

  def __init__(self, download_helper_object, project_name):
    """Initializes the source package helper.

    Args:
      download_helper_object: the download helper (instance of DownloadHelper).
      project_name: the name of the project.
    """
    super(SourcePackageHelper, self).__init__(project_name)
    self._download_helper = download_helper_object
    self._project_version = None
    self._source_filename = None

  @property
  def project_version(self):
    """The project version."""
    if not self._project_version:
      self._project_version = self._download_helper.GetLatestVersion(
          self.project_name)
    return self._project_version

  def Clean(self):
    """Removes previous versions of source packages and directories."""
    if not self.project_version:
      return

    filenames_to_ignore = re.compile(
        u'^{0:s}-.*{1!s}'.format(self.project_name, self.project_version))

    # Remove previous versions of source packages in the format:
    # project-*.tar.gz
    filenames = glob.glob(u'{0:s}-*.tar.gz'.format(self.project_name))
    for filename in filenames:
      if not filenames_to_ignore.match(filename):
        logging.info(u'Removing: {0:s}'.format(filename))
        os.remove(filename)

    # Remove previous versions of source directories in the format:
    # project-{version}
    filenames = glob.glob(u'{0:s}-*'.format(self.project_name))
    for filename in filenames:
      if os.path.isdir(filename) and not filenames_to_ignore.match(filename):
        logging.info(u'Removing: {0:s}'.format(filename))
        shutil.rmtree(filename)

  def Create(self):
    """Creates the source directory from the source package.

    Returns:
      The name of the source directory if successful or None on error.
    """
    if not self._source_filename:
      _ = self.Download()

    if not self._source_filename or not os.path.exists(self._source_filename):
      return

    archive = tarfile.open(self._source_filename, 'r:gz', encoding='utf-8')
    directory_name = ''

    for tar_info in archive.getmembers():
      filename = getattr(tar_info, u'name', None)
      try:
        filename = filename.decode(self.ENCODING)
      except UnicodeDecodeError:
        logging.warning(
            u'Unable to decode filename in tar file: {0:s}'.format(
                self._source_filename))
        continue

      if filename is None:
        logging.warning(u'Missing filename in tar file: {0:s}'.format(
            self._source_filename))
        continue

      if not directory_name:
        # Note that this will set directory name to an empty string
        # if filename start with a /.
        directory_name, _, _ = filename.partition(u'/')
        if not directory_name or directory_name.startswith(u'..'):
          logging.error(
              u'Unsuppored directory name in tar file: {0:s}'.format(
                  self._source_filename))
          return
        if os.path.exists(directory_name):
          break
        logging.info(u'Extracting: {0:s}'.format(self._source_filename))

      elif not filename.startswith(directory_name):
        logging.warning(
            u'Skipping: {0:s} in tar file: {1:s}'.format(
                filename, self._source_filename))
        continue

      archive.extract(tar_info)
    archive.close()

    return directory_name

  def Download(self):
    """Downloads the source package.

    Returns:
      The filename of the source package if successful also if the file was
      already downloaded or None on error.
    """
    if not self._source_filename:
      if not self.project_version:
        return

      self._source_filename = self._download_helper.Download(
          self.project_name, self.project_version)

    return self._source_filename

  def GetProjectIdentifier(self):
    """Retrieves the project identifier for a given project name.

    Returns:
      The project identifier or None on error.
    """
    return self._download_helper.GetProjectIdentifier(self.project_name)
