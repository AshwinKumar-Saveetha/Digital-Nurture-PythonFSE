import { Routes } from '@angular/router';

import { CourseList } from './course-list/course-list';
import { StudentProfile } from './student-profile/student-profile';

export const routes: Routes = [
  {
    path: '',
    component: CourseList,
    title: 'Courses | Student Portal'
  },
  {
    path: 'profile',
    component: StudentProfile,
    title: 'Profile | Student Portal'
  },
  {
    path: '**',
    redirectTo: ''
  }
];