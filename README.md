# Практикум по промышленной разработке ПО

## Касьянов Павел, Б05-103

### Домашнее задание №1

Для доступа к приложению после развертывания выполните команду:

```
kubectl port-forward service/journal-service 8080:80
```

Затем откройте http://localhost:8080 в браузере

### Домашние задания №2 и #3

Для доступа к приложению после развертывания выполните команду:

```
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80"
```

Затем откройте http://localhost:8080 в браузере

Для проверки метрик приложения используйте команду:

```
curl http://localhost:8080/metrics
```

Для доступа к Prometheus используйте команду:

```
kubectl port-forward -n journal-system svc/prometheus 9000:9000
```

Затем откройте в браузере http://localhost:9000

Метрики приложения в Prometheus:

```
journal_log_requests_total
```

Метрики Istio:

```
istio_requests_total
```
