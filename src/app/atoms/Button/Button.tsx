import styles from './Button.module.css';

interface ButtonProps {
    label: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary' | 'danger' | 'midlarge';
    size?: 'small' | 'medium' | 'large';
    disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
    label,
    onClick,
    variant = 'primary',   
    size = 'medium',       
    disabled = false
  }) => {
    const classNames = `${styles.button} ${styles[variant]} ${styles[size]} ${disabled ? styles.disabled : ''}`;
  
    return (
        <button
          className={classNames}
          onClick={onClick}
          disabled={disabled}
        >
          {label}
        </button>
      );
    };
    
    export default Button;