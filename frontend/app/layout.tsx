import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'proyecto 2',
  description: 'Created with v0',
  generator: 'v0.dev',
  icons: {
    icon: '/favicon.ico',  // Ruta correcta al favicon dentro de la carpeta 'public'
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  )
}
