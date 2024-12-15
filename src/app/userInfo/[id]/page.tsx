import React from 'react'
import UserHeader from '../../molecules/user_header/userHeader'
import UserInfo from '../../molecules/user_info/userInfo'
import WorkingInfo from '../../molecules/workingInfo/WorkingInfo'
import UserRating from '../../molecules/user_rating/UserRating'

export default function page() {
  return (
    <div>
      <UserHeader />
      <UserInfo />
      <WorkingInfo />
      <UserRating />
    </div>
  )
}
