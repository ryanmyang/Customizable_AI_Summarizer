import Image from 'next/image'
import React from 'react';
import CallMainButton from './components/CallMainButton';
import FileDropdown from './components/FileDropDown';

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <CallMainButton/>
        <FileDropdown/>
      </div>
    </main>
  )
}
