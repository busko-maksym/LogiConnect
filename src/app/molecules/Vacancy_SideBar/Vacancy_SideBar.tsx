'use client';

import { useState } from 'react';
import styles from './Vacancy_SideBar.module.css'
import Input from '@/app/atoms/Input/Input';
import Button from '@/app/atoms/Button/Button';
import Line from './img/Line 6.png'
import Image from 'next/image';

export default function Vacancy_SideBar({ onFilterChange }) {
  const [filters, setFilters] = useState({
    minSalary: '',
    maxSalary: '',
    activeInput: 'minSalary',
    minDistance: '',
    maxDistance: '',
    maxWeight: '',
    maxVolume: '',
    urgency: [],
  });

  const handleSliderChange = (e) => {
    const value = Number(e.target.value);

    // Перевіряємо, який інпут активний
    if (filters.activeInput === 'minSalary') {
      if (value <= filters.maxSalary) { // Перевірка на максимальний поріг
        setFilters((prevFilters) => ({
          ...prevFilters,
          minSalary: value,
        }));
      }
    } else if (filters.activeInput === 'maxSalary') {
      if (value >= filters.minSalary) { // Перевірка на мінімальний поріг
        setFilters((prevFilters) => ({
          ...prevFilters,
          maxSalary: value,
        }));
      }
    }
  };


  const handleInputFocus = (inputName) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      activeInput: inputName, // Встановлюємо, який інпут зараз активний
    }));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const handleCheckboxChange = (e) => {
    const { value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      urgency: prevFilters.urgency.includes(value)
        ? prevFilters.urgency.filter((item) => item !== value)
        : [...prevFilters.urgency, value],
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onFilterChange(filters);
  };

  return (
    <div className={styles.container}>
      <h1>Фільтр</h1>
      <h2>Шлях</h2>
      <form onSubmit={handleSubmit} className={styles.filters}>
      <div className={styles.row}>
      <Input
          label="Мінімальна відстань (км)"
          name="minDistance"
          type="number"
          placeholder="Введіть мінімальну відстань"
          value={filters.minDistance}
          onChange={handleInputChange}
          size="verysmall"
        />
        <Image src={Line}/>
        <Input
          label="Максимальна відстань (км)"
          name="maxDistance"
          type="number"
          placeholder="Введіть максимальну відстань"
          value={filters.maxDistance}
          onChange={handleInputChange}
          size="verysmall"
        />
        </div>
         <div className={styles.checkboxContainer}>
          <label>Терміновість</label>
          <div className={styles.checkboxes}>
            <input
              type="checkbox"
              value="High"
              checked={filters.urgency.includes('High')}
              onChange={handleCheckboxChange}
            />
            <span>Терміновість</span>
          </div>
          <div className={styles.checkboxes}>
            <input
              type="checkbox"
              value="Medium"
              checked={filters.urgency.includes('Medium')}
              onChange={handleCheckboxChange}
            />
            <span>Бажано швидше</span>
          </div>
          <div className={styles.checkboxes}>
            <input
              type="checkbox"
              value="Low"
              checked={filters.urgency.includes('Low')}
              onChange={handleCheckboxChange}
            />
            <span>Не терміново</span>
          </div>
        </div>
        <h3>Заробітня плата</h3>
        <div className={styles.salaryRange}>
          {/* Мінімальна зарплата */}
          <Input
            label=""
            name="minSalary"
            type="number"
            placeholder="Введіть мінімальну зарплату"
            value={filters.minSalary}
            onChange={handleInputChange}
            onFocus={() => handleInputFocus('minSalary')} // Встановлюємо активний інпут
            size="DaNyBlyaAndriy"
          />
          <span>--</span>
          {/* Максимальна зарплата */}
          <Input
            label=""
            name="maxSalary"
            type="number"
            placeholder="Введіть максимальну зарплату"
            value={filters.maxSalary}
            onChange={handleInputChange}
            onFocus={() => handleInputFocus('maxSalary')} // Встановлюємо активний інпут
            size="DaNyBlyaAndriy"
          />
        </div>

        {/* Слайдер */}
        <div className={styles.sliderContainer}>
          <input
            type="range"
            min="0"
            max="10000"
            value={filters.activeInput === 'minSalary' ? filters.minSalary : filters.maxSalary}
            onChange={handleSliderChange}
            step="10"
            className={styles.slider}
          />
        </div>
    <div className={styles.aboutProduct}>
        <Input
          label="Максимальна вага"
          name="maxWeight"
          type="number"
          placeholder="Введіть максимальну вагу"
          value={filters.maxWeight}
          onChange={handleInputChange}
          size="small"
        />
        <Input
          label="Максимальний об'єм"
          name="maxVolume"
          type="number"
          placeholder="Введіть максимальний об'єм"
          value={filters.maxVolume}
          onChange={handleInputChange}
          size="small"
        />
        <Button
          label="Застосувати фільтри"
          onClick={handleSubmit}
          className={styles.acceptFilter}
          variant="primary"
          size=''
        />
        </div>
      </form>
    </div>
  );
}
