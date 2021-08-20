import time
import psutil
from h2o_wave import site, ui, data

page = site['/sys']

card_header = page.add('header', ui.header_card(
    box='1 1 3 1',    # x座標 y座標 幅 高さ
    title='System Monitoring',
    subtitle='Wave実行環境のSystem Monitoring',
))
cpu_card = page.add('cpu_stats', ui.small_series_stat_card(
    box='1 2 2 1',
    title='CPU',
    value='={{usage}}%',
    data=dict(usage=0.0),
    plot_data=data('tick usage', -15),
    plot_category='tick',
    plot_value='usage',
    plot_zero_value=0,
    plot_color='$red',
))
mem_card = page.add('mem_stats', ui.small_series_stat_card(
    box='1 3 2 1',
    title='Memory',
    value='={{usage}}%',
    data=dict(usage=0.0),
    plot_data=data('tick usage', -15),
    plot_category='tick',
    plot_value='usage',
    plot_zero_value=0,
    plot_color='$blue',
))
disk_card = page.add('disk_status', ui.tall_gauge_stat_card(
    box='3 2 1 2',
    title='Disk',
    value='={{intl foo minimum_fraction_digits=2 maximum_fraction_digits=2}}GB',
    aux_value='={{intl bar minimum_fraction_digits=2 maximum_fraction_digits=2}}%',
    plot_color='$green',
    progress=0,
    data=dict(foo=0, bar=0),
))

tick = 0
while True:
    tick += 1

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_card.data.usage = cpu_usage
    cpu_card.plot_data[-1] = [tick, cpu_usage]

    mem_usage = psutil.virtual_memory().percent
    mem_card.data.usage = mem_usage
    mem_card.plot_data[-1] = [tick, mem_usage]

    disk_usage = psutil.disk_usage(path='/').percent
    gb = 1024 * 1024 * 1024
    disk_usage_gb = psutil.disk_usage(path='/').used / gb
    disk_card.data.foo = disk_usage_gb
    disk_card.data.bar = disk_usage
    disk_card.progress = disk_usage / 100

    page.save()
    time.sleep(2)