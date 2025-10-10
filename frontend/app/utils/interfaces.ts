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
