package services

import (
	"context"
	"log"
	"time"

	"attendanceservice/internal/application/usecases"
	"attendanceservice/internal/domain/repositories"
)

// QRSchedulerService servicio para manejar la programación automática de códigos QR
type QRSchedulerService struct {
	qrRepo    repositories.QRCodeRepository
	qrUseCase *usecases.QRCodeUseCase
	stopChan  chan bool
}

// NewQRSchedulerService crea una nueva instancia del servicio programador de QR
func NewQRSchedulerService(qrRepo repositories.QRCodeRepository, qrUseCase *usecases.QRCodeUseCase) *QRSchedulerService {
	return &QRSchedulerService{
		qrRepo:    qrRepo,
		qrUseCase: qrUseCase,
		stopChan:  make(chan bool),
	}
}

// Start inicia el servicio de programación de códigos QR
func (s *QRSchedulerService) Start(ctx context.Context) {
	log.Println("🕒 QR Scheduler Service iniciado - Los códigos QR se regenerarán cada 15 segundos")
	
	// Ticker para verificar códigos expirados cada 5 segundos
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			log.Println("🕒 QR Scheduler Service detenido por contexto")
			return
		case <-s.stopChan:
			log.Println("🕒 QR Scheduler Service detenido manualmente")
			return
		case <-ticker.C:
			s.expireOldQRCodes(ctx)
		}
	}
}

// Stop detiene el servicio de programación
func (s *QRSchedulerService) Stop() {
	close(s.stopChan)
}

// expireOldQRCodes marca como expirados los códigos QR antiguos
func (s *QRSchedulerService) expireOldQRCodes(ctx context.Context) {
	err := s.qrUseCase.ExpireOldQRCodes(ctx)
	if err != nil {
		log.Printf("❌ Error al expirar códigos QR antiguos: %v", err)
	}
}
