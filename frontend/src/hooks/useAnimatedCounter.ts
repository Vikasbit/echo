import { useEffect, useState } from 'react';

interface AnimatedCounterOptions {
  end: number;
  duration?: number;
  start?: number;
  suffix?: string;
  prefix?: string;
  decimals?: number;
}

export function useAnimatedCounter(
  isActive: boolean,
  options: AnimatedCounterOptions
) {
  const { end, duration = 2000, start = 0, suffix = '', prefix = '', decimals = 0 } = options;
  const [value, setValue] = useState(start);

  useEffect(() => {
    if (!isActive) return;

    let startTime: number | null = null;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = start + (end - start) * eased;

      setValue(Number(current.toFixed(decimals)));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [isActive, end, duration, start, decimals]);

  const formatted = `${prefix}${value.toLocaleString()}${suffix}`;

  return { value, formatted };
}
