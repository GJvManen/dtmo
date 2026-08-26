import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { AdministrationSecurityAudit } from './AdministrationSecurityAudit';
import { AdministrationWorkspace } from './AdministrationWorkspace';
import { BundledPlatformReadiness } from './BundledPlatformReadiness';
import { FrameworkIntegrationReadiness } from './FrameworkIntegrationReadiness';
import { App } from './App';
import './styles.css';
import './command-center.css';
import './unified-intelligence.css';

function installCanonicalLocalDevelopmentAuthContext() {
  const nativeFetch = window.fetch.bind(window);
  window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
    const requestUrl = input instanceof Request ? input.url : input.toString();
    const resolvedUrl = new URL(requestUrl, window.location.origin);
    if (resolvedUrl.origin !== window.location.origin) {
      return nativeFetch(input, init);
    }

    const headers = new Headers(input instanceof Request ? input.headers : undefined);
    new Headers(init?.headers).forEach((value, key) => headers.set(key, value));

    if (!headers.has('X-DTMO-Subject')) {
      headers.set('X-DTMO-Subject', sessionStorage.getItem('dtmo.subject') || 'admin-tester');
    }
    if (!headers.has('X-DTMO-Roles')) {
      headers.set('X-DTMO-Roles', sessionStorage.getItem('dtmo.roles') || 'admin');
    }
    if (!headers.has('X-DTMO-API-Key')) {
      headers.set('X-DTMO-API-Key', sessionStorage.getItem('dtmo.apiKey') || '');
    }

    return nativeFetch(input, { ...init, headers });
  };
}

installCanonicalLocalDevelopmentAuthContext();

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter basename="/workbench">
        <Routes>
          <Route path="/administration" element={<><AdministrationWorkspace /><BundledPlatformReadiness /><FrameworkIntegrationReadiness /><AdministrationSecurityAudit /></>} />
          <Route path="*" element={<App />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
);