from clint.textui.progress import Bar as ProgressBar


def create_callback(encoder):
  bar = ProgressBar(expected_size=encoder.len, filled_char='=')

  def callback(monitor):
    bar.show(monitor.bytes_read)

  return callback
