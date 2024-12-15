import React, { useState } from 'react';
import styles from './TransportationOwner.module.css';
import Input from '@/app/atoms/Input/Input';
import axios from 'axios';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export default function TransportationOwner() {
    const [isChecked, setIsChecked] = useState(false);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [fleetSize, setFleetSize] = useState(0);
    const [vehicleTypes, setVehicleTypes] = useState('');
    const [operationArea, setOperationArea] = useState('');
    const [specialPermits, setSpecialPermits] = useState('');

    const [alertOpen, setAlertOpen] = useState(false);
        const [alertMessage, setAlertMessage] = useState('');
        const [alertSeverity, setAlertSeverity] = useState<'success' | 'error'>('success');

    const handleCheckBoxChange = () => {
        setIsChecked(!isChecked);
    };

    const handleSubmit = async () => {
        const requestData = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            acc_status: "company",
            company_name: companyName,
            fleet_size: fleetSize,
            vehicle_types: vehicleTypes.split(','),
            operation_area: operationArea,
            special_permits: specialPermits.split(',')
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/user/register/transportcompany', requestData);
            setAlertMessage('Ви успішно зареєструвались!');
            setAlertSeverity('success');
            setAlertOpen(true);
            console.log("Response:", response.data);
        } catch (error) {
            console.error("Error during registration:", error);
            setAlertMessage('Помилка реєстрації: ' + (error.response?.data.msg || 'Невідома помилка'));
            setAlertSeverity('error');
            setAlertOpen(true);
        }
    };

    const handleCloseAlert = () => {
        setAlertOpen(false);
    };
    return (
        <div>
            <div className={styles.container_second}>
                <div className={styles.Text}>
                    <h1>Крок №2</h1>
                </div>
                <div className={styles.row}>
                    <div className={styles.column}>
                        <Input 
                            label="Ім’я"
                            placeholder="Ім’я"
                            value={firstName}
                            onChange={(e) => setFirstName(e.target.value)}
                        />
                        <Input 
                            label="Прізвище"
                            placeholder="Прізвище"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                        />
                    </div>
                    <div className={styles.column}>
                        <Input 
                            label="Пароль"
                            placeholder="Пароль"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Input
                            label="Електронна пошта"
                            placeholder="Електронна пошта"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                </div>
            </div>
            <div className={styles.container_third}>
                <div className={styles.Text}>
                    <h1>Крок №3</h1>
                </div>
                <div className={styles.row}>
                    <div className={styles.column}>
                        <Input 
                            label="Назва компанії"
                            placeholder="Назва компанії"
                            value={companyName}
                            onChange={(e) => setCompanyName(e.target.value)}
                        />
                        <Input 
                            label="Географічна діяльність"
                            placeholder="Географічна діяльність"
                            value={operationArea}
                            onChange={(e) => setOperationArea(e.target.value)}
                        />
                    </div>
                    <div className={styles.column}>
                        <Input 
                            label="Наявність спеціальних дозволів або сертифікатів"
                            placeholder="Наявність спеціальних дозволів або сертифікатів"
                            value={specialPermits}
                            onChange={(e) => setSpecialPermits(e.target.value)}
                        />
                        <Input
                            label="Типи транспортних засобів"
                            placeholder="Типи транспортних засобів (через кому)"
                            value={vehicleTypes}
                            onChange={(e) => setVehicleTypes(e.target.value)}
                        />
                        <Input
                            label="Кількість транспортних засобів у флоті"
                            placeholder="Кількість транспортних засобів у флоті"
                            type="number"
                            value={fleetSize}
                            onChange={(e) => setFleetSize(Number(e.target.value))}
                        />
                    </div>
                </div>
            </div>
            <div className={styles.container_fourth}>
                <div className={styles.Text}>
                    <h1>Крок №4</h1>
                </div>
                <div className={styles.confirm}>
                    <input 
                        type='checkbox'
                        id='terms'
                        checked={isChecked}
                        onChange={handleCheckBoxChange}
                        className={isChecked ? styles.activeInput : styles.inactiveInput}
                    />
                    <label>Я погоджуюсь з умовами використання та політикою <br />конфіденційності</label>
                    <button
                        className={isChecked ? styles.activeButton : styles.disabledButton}
                        onClick={handleSubmit}
                        disabled={!isChecked}
                    >
                        Завершити реєстрацію
                    </button>
                </div>
            </div>
            <Snackbar
                open={alertOpen}
                autoHideDuration={8000}
                onClose={handleCloseAlert}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                        >
                <Alert
                    onClose={handleCloseAlert}
                    severity={alertSeverity}
                    variant="outlined"
                            >
                    {alertMessage}
                </Alert>
            </Snackbar>
        </div>
    );
}
