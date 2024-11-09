import React from 'react'
import Vacancy_Header from '../molecules/Vacancy-Header/Vacancy_Header'
import Vacancy_SideBar from '../molecules/Vacancy_SideBar/Vacancy_SideBar'
import Vacancy_Search from '../molecules/Vacancy_Search/Vacancy_Search'
import Vacancy_Block from '../molecules/Vacancy_Block/Vacancy_Block'

export default function VacancyPage() {
  return (
    <div>
      <Vacancy_Header />
      <Vacancy_SideBar />
      <Vacancy_Search />
      <Vacancy_Block />
    </div>
  )
}
