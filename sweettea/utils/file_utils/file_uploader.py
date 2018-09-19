from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from sweettea import log
from sweettea.utils.file_utils import get_file_ext, get_mime_type


class FileUploader(object):

  def __init__(self, api, default_name='file', default_completion_msg='Done!'):
    self.api = api
    self.default_name = default_name
    self.default_completion_msg = default_completion_msg

  def upload(self, api_route, file_path, name=None, payload=None, completion_msg=None):
    name = name or self.default_name
    payload = payload or {}

    # Get file extension from path.
    file_ext = get_file_ext(file_path)

    # Append extension to name if extension exists.
    if file_ext:
      name = name + '.' + file_ext

    # Add file info to payload.
    payload['file'] = (name, open(file_path, 'rb'), get_mime_type(file_path))
    payload['ext'] = file_ext

    # Create a multipart encoder.
    encoder = MultipartEncoder(fields=payload)

    # Create progress callback, specifying message to show when upload completes.
    callback = self._progress_display_cb(encoder, completion_msg=completion_msg)

    # Return monitor to track upload progress.
    monitor = MultipartEncoderMonitor(encoder, callback)

    try:
      # Upload model and display progress.
      self.api.post(api_route,
                    headers={'Content-Type': monitor.content_type},
                    mp_upload_monitor=monitor)
    except KeyboardInterrupt:
      exit()

  def _progress_display_cb(self, encoder, completion_msg=None):
    """
    Create a progress callback function for a multi-part file upload

    :param encoder:
      Multipart file encoder
      :type: requests_toolbelt.multipart.encoder.MultipartEncoder
    :param str completion_msg:
      Log to display when the file upload has completed
    :return: Upload progress callback function
    :rtype: function
    """
    completion_msg = completion_msg or self.default_completion_msg

    # Create a progress bar with the given size, specifying which character to show for progress.
    bar = ProgressBar(expected_size=encoder.len, filled_char='=')

    # Function to be called as the upload progresses
    def callback(monitor):
      # If upload has completed...
      if monitor.bytes_read == encoder.len:
        # Hacking around this callback being called twice when completed.
        if not hasattr(monitor, 'finished'):
          setattr(monitor, 'finished', True)

          # Show upload progress.
          bar.show(monitor.bytes_read)

          # Display completion log if provided.
          if completion_msg:
            log(completion_msg)
      else:
        # Show upload progress.
        bar.show(monitor.bytes_read)

    return callback
