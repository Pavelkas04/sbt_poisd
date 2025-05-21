#!/bin/bash

echo "Сборка docker образа"
docker build -t journal-service:latest .

echo "Загрузка образа в Minikube"
minikube image load journal-service:latest

echo "Создание конфигурации"
kubectl apply -f k8s/configuration.yaml

echo "Развертывание тестового пода"
kubectl apply -f k8s/pod.yaml

echo "Проверяем готовность пода"
kubectl wait --for=condition=Ready pod/journal-test-pod --timeout=60s

echo "Проверка API"
kubectl exec journal-test-pod -- curl -s http://localhost:8000/status

echo "Развертывание приложения"
kubectl apply -f k8s/deployment.yaml

echo "Ожидание готовности приложения"
kubectl wait --for=condition=Available deployment/journal-deployment --timeout=90s

echo "Создание сервиса для балансировки нагрузки"
kubectl apply -f k8s/journal-service.yaml

echo "Настройка хранилища"
kubectl apply -f k8s/storage-volume.yaml
kubectl apply -f k8s/storage-claim.yaml

echo "Развертывание сборщика журналов"
kubectl apply -f k8s/daemonset-collector.yaml

echo "Настройка периодического архивирования"
kubectl apply -f k8s/cronjob.yaml

echo "Развертывание успешно завершено!"


