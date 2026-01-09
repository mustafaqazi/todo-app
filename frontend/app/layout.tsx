import type { Metadata, Viewport } from 'next'
import '@/styles/globals.css'
import '@/styles/animations.css'
import RootLayoutClient from '@/components/RootLayoutClient'
import { Toaster } from '@/components/ui/toaster'

export const metadata: Metadata = {
  title: 'Premium TODO App - Task Management Made Beautiful',
  description:
    'Transform your tasks into achievements with our premium, minimalist task management application. Beautiful dark/light mode, real-time updates, and intelligent filtering.',
  keywords: ['todo', 'task management', 'productivity', 'next.js', 'react'],
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <RootLayoutClient>
          {children}
          <Toaster />
        </RootLayoutClient>
      </body>
    </html>
  )
}
