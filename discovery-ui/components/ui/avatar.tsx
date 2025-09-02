import { cn } from '@/lib/utils';

interface AvatarProps {
  name: string;
  email: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function Avatar({ name, email, size = 'md', className }: AvatarProps) {
  // Get first letter of name or email
  const initial = (name || email || 'U').charAt(0).toUpperCase();

  // Generate consistent color based on email
  const colors = [
    'bg-blue-500', 'bg-green-500', 'bg-purple-500',
    'bg-red-500', 'bg-yellow-500', 'bg-pink-500',
    'bg-indigo-500', 'bg-teal-500'
  ];
  const colorIndex = email ? email.length % colors.length : 0;
  const bgColor = colors[colorIndex];

  const sizeClasses = {
    sm: 'w-6 h-6 text-xs',
    md: 'w-8 h-8 text-sm',
    lg: 'w-10 h-10 text-base'
  };

  return (
    <div
      className={cn(
        'rounded-full flex items-center justify-center text-white font-semibold',
        bgColor,
        sizeClasses[size],
        className
      )}
    >
      {initial}
    </div>
  );
}
