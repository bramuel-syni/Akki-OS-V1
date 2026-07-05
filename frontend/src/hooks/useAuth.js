/**
 * useAuth — Phase 8 Stage B-1 auth context + hook.
 *
 * Provides three states:
 *   - null (checking)  — on mount, calling /api/auth/me to introspect
 *   - Identity object  — authenticated
 *   - false            — not authenticated
 *
 * Federation-forward: replacing the JWT auth adapter with OAuth (post-Phase-8)
 * requires zero changes at this seam — this hook consumes `/api/auth/me` and
 * the token store abstraction, both of which the OAuth adapter re-implements.
 */
import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import api, { tokenStore } from '../apiClient';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [identity, setIdentity] = useState(null); // null = checking, object = authed, false = anon

  const checkSession = useCallback(async () => {
    const tok = tokenStore.getAccessToken();
    if (!tok) {
      setIdentity(false);
      return;
    }
    const { status, body } = await api.authMe();
    if (status === 200) {
      setIdentity(body);
    } else if (status === 401) {
      // Try refresh once
      const rt = tokenStore.getRefreshToken();
      if (rt) {
        const refreshed = await api.authRefresh();
        if (refreshed.status === 200) {
          tokenStore.setTokens(refreshed.body);
          setIdentity(refreshed.body.identity);
          return;
        }
      }
      tokenStore.clear();
      setIdentity(false);
    } else {
      setIdentity(false);
    }
  }, []);

  useEffect(() => {
    checkSession();
  }, [checkSession]);

  const login = useCallback(async (email, password) => {
    const { status, body } = await api.authLogin(email, password);
    if (status === 200) {
      tokenStore.setTokens(body);
      setIdentity(body.identity);
      return { ok: true };
    }
    return { ok: false, status, body };
  }, []);

  const register = useCallback(async (email, password, name) => {
    const { status, body } = await api.authRegister(email, password, name);
    if (status === 201) {
      tokenStore.setTokens(body);
      setIdentity(body.identity);
      return { ok: true };
    }
    return { ok: false, status, body };
  }, []);

  const logout = useCallback(() => {
    tokenStore.clear();
    setIdentity(false);
  }, []);

  return (
    <AuthContext.Provider value={{ identity, login, register, logout, checkSession }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
