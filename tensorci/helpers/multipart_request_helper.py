from io import BytesIO
from clint.textui.progress import Bar as ProgressBar


def create_callback(encoder):
  bar = ProgressBar(expected_size=encoder.len, filled_char='=')

  def callback(monitor):
    bar.show(monitor.bytes_read)

  return callback


class ProgressDownloadStream(BytesIO):

  def __init__(self, expected_size=None, save_to=None):
    super(BytesIO, self).__init__(self)
    self.prog_bar = ProgressBar(expected_size=expected_size, filled_char='=')
    self.progress = 0
    self.f = open(save_to, 'wb')

  def write(self, chunk):
    super(BytesIO, self).write(chunk)
    self.f.write(chunk)

    self.progress += int(len(chunk))
    self.prog_bar.show(self.progress)

  def close(self):
    super(BytesIO, self).close()
    self.f.close()