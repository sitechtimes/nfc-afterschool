export interface ScanInstance {
  date: string;
  activity: string;
  student_name: string;
  student_email: string;
  student_cassid: Int16Array;
}

export interface User {
  username: string;
  role: string;
}
