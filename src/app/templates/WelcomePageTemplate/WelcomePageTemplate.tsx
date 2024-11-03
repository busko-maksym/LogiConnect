import React from 'react'
import Header from '../../organisms/Header/Header'
import Welcome from '../../molecules/Welcome/Welcome'
import Suggestion from '../../molecules/Suggestion/Suggestion'
import OurGoal from '../../molecules/OurGoal/OurGoal'
import InfoSlogan from '../../molecules/Info_slogan/InfoSlogan'
import RegisterSuggestion from '../../molecules/RegisterSuggestion/RegisterSuggestion'
import Footer from '../../organisms/Footer/Footer'

export default function WelcomePageTemplate() {
  return (
    <div>
      <Header />
      <Welcome />
      <Suggestion />
      <OurGoal />
      <InfoSlogan />
      <RegisterSuggestion />
      <Footer />
    </div>
  )
}
