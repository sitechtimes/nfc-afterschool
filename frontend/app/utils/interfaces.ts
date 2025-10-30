export interface ScanInstance {
  date: string;
  activity: string;
  student_name: string;
  student_email: string;
  student_cassid: Int16Array;
}

export interface SearchParams {
  searchString: string;
  searchType: string;
  searchDate: string;
}
export interface User {
  username: string;
  role: string;
}

export interface StudentLookup {
  Name: string;
  Homeroom: string;
  gradYear: number;
  Email: string;
  caassID: string;
  OSIS: string;
}
