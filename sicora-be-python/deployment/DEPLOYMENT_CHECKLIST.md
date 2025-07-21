# ✅ Checklist de Deployment SICORA Backend

## Pre-Deployment
- [ ] Tests de integración pasan localmente
- [ ] Configuraciones validadas
- [ ] Variables de entorno configuradas
- [ ] Paquete de deployment creado

## VPS Setup
- [ ] Ubuntu actualizado
- [ ] Docker instalado
- [ ] Docker Compose instalado
- [ ] Nginx instalado
- [ ] Firewall configurado (puertos 22, 80, 443)
- [ ] Usuario con permisos docker

## Deployment
- [ ] Archivos transferidos al VPS
- [ ] Variables de entorno configuradas
- [ ] Servicios desplegados con docker-compose
- [ ] Nginx configurado
- [ ] SSL configurado (opcional)

## Validation
- [ ] Health checks responden
- [ ] Documentación Swagger accesible
- [ ] Base de datos conecta
- [ ] Redis funciona
- [ ] Logs sin errores críticos

## Monitoring Setup
- [ ] Scripts de monitoreo instalados
- [ ] Backups automáticos configurados
- [ ] Cron jobs configurados
- [ ] Alertas básicas configuradas

## URLs a Validar
- [ ] http://TU_DOMINIO/health/api
- [ ] http://TU_DOMINIO/health/notification
- [ ] http://TU_DOMINIO/api/docs
- [ ] http://TU_DOMINIO/notifications/docs

## Post-Deployment
- [ ] Monitoreo funcionando
- [ ] Backup inicial creado
- [ ] Documentación actualizada
- [ ] Frontend puede conectar
