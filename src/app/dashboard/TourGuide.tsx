'use client'
import { useState, useEffect } from 'react'

export default function TourGuide({ view }: { view: string }) {
  const [run, setRun] = useState(false)
  const [stepIndex, setStepIndex] = useState(0)
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null)

  const steps: Record<string, { target: string, text: string }[]> = {
    tapechart: [
      { target: '.tour-tapechart-metrics', text: 'Aquí ves las métricas clave de tu hotel en tiempo real: Ocupación, habitaciones sucias y más.' },
      { target: '.tour-tapechart-rooms', text: 'En esta tabla verás todas las habitaciones disponibles. Haz clic en "Reservar" para registrar la llegada de un huésped o planear una reserva futura.' },
      { target: '.tour-tapechart-res', text: 'Aquí aparecerá la lista de todas las reservas activas (las que están corriendo en este momento).' }
    ],
    housekeeping: [
      { target: '.tour-housekeeping-list', text: 'Cuando un huésped hace check-out, la habitación pasa a estar "Sucia". Tu personal de limpieza verá la lista aquí y podrá marcarla como "Limpia" cuando termine.' }
    ],
    cashshift: [
      { target: '.tour-cash-form', text: 'Al final de su turno, el recepcionista ingresa el efectivo en caja. El sistema compara esto con las reservas cobradas para detectar si falta dinero (Arqueo Ciego).' }
    ],
    crm: [
      { target: '.tour-crm-list', text: 'Todos los huéspedes que se registran quedan guardados aquí. Puedes ver sus puntos de lealtad y su nivel (Bronce, Plata, Oro).' }
    ],
    users: [
      { target: '.tour-users-form', text: 'Crea accesos para tus empleados aquí. Elige el rol adecuado (ej. Recepción) para que solo vean lo que les corresponde.' }
    ],
    settings: [
      { target: '.tour-settings', text: 'Administra tus sucursales, define tus tipos de habitación (con precios por noche y hora) y finalmente crea las habitaciones físicas.' }
    ]
  }

  const currentSteps = steps[view] || []
  const currentStep = currentSteps[stepIndex]

  useEffect(() => {
    if (!run || !currentStep) return
    const updatePosition = () => {
      const el = document.querySelector(currentStep.target)
      if (el) {
        setTargetRect(el.getBoundingClientRect())
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }
    updatePosition()
    window.addEventListener('resize', updatePosition)
    return () => window.removeEventListener('resize', updatePosition)
  }, [run, stepIndex, currentStep])

  const nextStep = () => {
    if (stepIndex < currentSteps.length - 1) {
      setStepIndex(stepIndex + 1)
    } else {
      setRun(false)
      setStepIndex(0)
    }
  }

  const closeTour = () => {
    setRun(false)
    setStepIndex(0)
  }

  if (!run || !currentStep || !targetRect) {
    return (
      <button 
        onClick={() => { setRun(true); setStepIndex(0) }}
        style={{
          position: 'fixed', bottom: '20px', right: '20px', zIndex: 50,
          background: 'var(--orange)', color: '#fff', border: 'none',
          padding: '10px 15px', borderRadius: '20px', fontWeight: '800',
          cursor: 'pointer', boxShadow: '0 4px 12px rgba(255, 107, 0, 0.4)'
        }}
      >
        💡 Ver Tour
      </button>
    )
  }

  return (
    <>
      <div style={{ position: 'fixed', inset: 0, background: 'rgba(5, 10, 20, 0.6)', zIndex: 999 }} onClick={closeTour} />
      
      {/* Spotlight cutout */}
      <div style={{
        position: 'fixed',
        top: targetRect.top - 10,
        left: targetRect.left - 10,
        width: targetRect.width + 20,
        height: targetRect.height + 20,
        border: '3px solid var(--orange)',
        borderRadius: '16px',
        boxShadow: '0 0 0 9999px rgba(5, 10, 20, 0.6)',
        pointerEvents: 'none',
        zIndex: 1000,
        transition: 'all 0.3s ease'
      }} />

      {/* Tooltip */}
      <div style={{
        position: 'fixed',
        top: Math.max(20, targetRect.bottom + 15),
        left: Math.max(20, targetRect.left + (targetRect.width / 2) - 150),
        width: '300px',
        background: '#1a2235',
        border: '1px solid var(--orange)',
        borderRadius: '12px',
        padding: '16px',
        color: '#fff',
        zIndex: 1001,
        boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
        transition: 'all 0.3s ease'
      }}>
        <div style={{ fontSize: '13px', lineHeight: '1.5', marginBottom: '16px' }}>
          {currentStep.text}
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-500)' }}>Paso {stepIndex + 1} de {currentSteps.length}</span>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={closeTour} style={{ background: 'none', border: 'none', color: '#9ca3af', cursor: 'pointer', fontSize: '12px' }}>Omitir</button>
            <button onClick={nextStep} style={{ background: 'var(--orange)', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '12px' }}>
              {stepIndex === currentSteps.length - 1 ? 'Terminar' : 'Siguiente'}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
