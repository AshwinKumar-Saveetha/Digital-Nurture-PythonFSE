import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface ApiCourse {
  userId: number;
  id: number;
  title: string;
  body: string;
}

@Injectable({
  providedIn: 'root'
})
export class CourseService {
  private readonly apiUrl =
    'https://jsonplaceholder.typicode.com/posts?_limit=5';

  constructor(private http: HttpClient) {}

  getCourses(): Observable<ApiCourse[]> {
    return this.http.get<ApiCourse[]>(this.apiUrl);
  }
}