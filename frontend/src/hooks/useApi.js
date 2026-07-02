import { useState, useEffect, useCallback } from 'react';

export function useApi(apiFn, deps = []) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const refetch = useCallback(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiFn()
      .then(d => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(e => {
        if (!cancelled) {
          setError(e.response?.data?.detail || e.message || 'Unknown error');
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    const cleanup = refetch();
    return cleanup;
  }, [refetch]);

  return { data, error, loading, refetch };
}
