import { CommonModule } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  OnInit
} from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CourseCard } from '../course-card/course-card';
import { ApiCourse, CourseService } from '../course';

@Component({
  selector: 'app-course-list',
  imports: [CommonModule, FormsModule, CourseCard],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css'
})
export class CourseList implements OnInit {
  searchTerm = '';
  loading = true;
  courses: ApiCourse[] = [];

  constructor(
    private courseService: CourseService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadCourses();
  }

  loadCourses(): void {
    this.loading = true;

    this.courseService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
        this.changeDetectorRef.detectChanges();
      },
      error: (error) => {
        console.error('Unable to load courses:', error);
        this.loading = false;
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  get filteredCourses(): ApiCourse[] {
    const searchValue = this.searchTerm.trim().toLowerCase();

    if (!searchValue) {
      return this.courses;
    }

    return this.courses.filter((course) =>
      course.title.toLowerCase().includes(searchValue)
    );
  }

  trackCourseById(index: number, course: ApiCourse): number {
    return course.id;
  }
}