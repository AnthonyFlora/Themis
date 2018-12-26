from Framework.Themis import EventProcessor
import threading
import subprocess


class PerformanceMonitor(EventProcessor):
    def __init__(self, event_broker, host):
        EventProcessor.__init__(self, event_broker)
        self.host = host
        self.processor = self.processor + '_' + host
        self.metric_params = []
        self.metric_values = []
        self.metrics = {}
        self.monitor_thread = threading.Thread(target=self.monitor_thread)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_thread(self):
        while True:
            self.log('monitor_thread starting..')
            try:
                process = subprocess.Popen(['ssh', 'pi@hyperion.local', 'sar', '-u', '-r', '5'], stdout=subprocess.PIPE)
                while True:
                    line = process.stdout.readline()
                    if line != '':
                        self.log(line.strip())
                        tokens = line.split()
                        if len(tokens) == 0:
                            self.metric_params = []
                            self.metric_values = []
                            self.metrics = {}
                        else:
                            if len(self.metric_params) == 0:
                                for token in tokens[2:]:
                                    self.metric_params.append(token)
                            else:
                                self.metrics['time'] = tokens[0] + ' ' + tokens[1]
                                for token in tokens[2:]:
                                    self.metric_values.append(token)
                                for i in range(len(self.metric_params)):
                                    self.metrics[self.metric_params[i]] = self.metric_values[i]
                                for k,v in self.metrics.iteritems():
                                    self.log('%s - %s' % (k, v))
                    else:
                        break
            except:
                self.log('monitor_thread stopped..')