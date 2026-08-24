'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase'

export default function LoginPage() {
  const router = useRouter()
  const supabase = createClient()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    const { error: authError } = await supabase.auth.signInWithPassword({
      email: username,
      password: password,
    })

    if (authError) {
      setError(authError.message === 'Invalid login credentials' ? 'Usuario o contraseña incorrectos.' : authError.message)
      setLoading(false)
    } else {
      router.push('/dashboard')
    }
  }

  return (
    <div style={{
      position: 'fixed', inset: 0,
      background: 'var(--bg-900)',
      backgroundImage: `
        radial-gradient(50% 50% at 50% 30%, rgba(255,107,0,0.15) 0%, transparent 80%),
        radial-gradient(circle at 1px 1px, rgba(255,255,255,0.04) 1px, transparent 0)
      `,
      backgroundSize: 'auto, 28px 28px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '16px',
    }}>
      <div className="animate-scaleIn" style={{
        background: 'rgba(13,21,39,0.9)',
        backdropFilter: 'blur(24px) saturate(180%)',
        border: '1px solid var(--border-card)',
        borderRadius: '24px',
        width: '100%',
        maxWidth: '420px',
        padding: '36px 30px',
        boxShadow: '0 25px 60px -15px rgba(0,0,0,0.8), 0 0 0 1px rgba(255,107,0,0.12)',
      }}>

        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
          <div className="animate-floatOrb" style={{
            width: '44px', height: '44px',
            background: 'linear-gradient(135deg, var(--orange) 0%, #c2410c 100%)',
            borderRadius: '13px',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 8px 24px var(--orange-glow)',
          }}>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 21h18M5 21V7l8-4v18M13 21V3l6 4v14"/>
            </svg>
          </div>
          <div>
            <div style={{ fontSize: '22px', fontWeight: '900', letterSpacing: '-0.04em', color: '#fff' }}>
              AURA<span style={{ color: 'var(--orange)' }}>.</span>PMS
            </div>
            <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '1px', color: 'var(--text-500)', fontFamily: "'JetBrains Mono', monospace" }}>
              ECOSISTEMA ÍMPETU HUB
            </div>
          </div>
        </div>

        <p style={{ fontSize: '13px', color: 'var(--text-300)', marginBottom: '22px', lineHeight: '1.5' }}>
          Ingresa tus credenciales para acceder al sistema hotelero.
        </p>

        {/* Error */}
        {error && (
          <div style={{
            background: 'rgba(239,68,68,0.12)',
            border: '1px solid rgba(239,68,68,0.35)',
            color: '#fca5a5',
            padding: '10px 14px',
            borderRadius: '10px',
            fontSize: '12.5px',
            marginBottom: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '14px' }}>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.6px', color: 'var(--text-500)', marginBottom: '6px' }}>
              Usuario
            </label>
            <input
              type="text"
              className="form-input"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Ingresa tu usuario..."
              autoComplete="username"
              required
            />
          </div>

          <div style={{ marginBottom: '22px' }}>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.6px', color: 'var(--text-500)', marginBottom: '6px' }}>
              Contraseña
            </label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••••••"
              autoComplete="current-password"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="tactile"
            style={{
              width: '100%',
              background: loading ? 'rgba(255,107,0,0.5)' : 'linear-gradient(135deg, var(--orange) 0%, #ea580c 100%)',
              color: '#fff',
              border: 'none',
              padding: '13px',
              borderRadius: '12px',
              fontSize: '13.5px',
              fontWeight: '700',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 6px 20px var(--orange-glow)',
              fontFamily: 'inherit',
            }}
          >
            {loading ? (
              <>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                </svg>
                Verificando...
              </>
            ) : (
              <>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M15 12H3"/>
                </svg>
                Acceder al Sistema
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  )
}
