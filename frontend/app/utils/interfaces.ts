export interface SearchParams {
  searchString: string;
  searchType: string;
  searchDate: string;
}

export interface StudentLookup {
  id: string;
  name: string;
  homeroom: string;
  gradYear: number;
  email: string;
  caassID: string;
  osis: string;
}

export interface Activity {
  id: string;
  name: string;
  type: string;
  time_start: string;
  time_end: string;
  restricted: boolean;
}

export interface ScanInstanceAPI {
  id: string;
  student: string;
  time: string;
  event: string;
}

export interface ScanInstance {
  id: string;
  studentName: string;
  studentEmail: string;
  studentOsis?: string;
  date: string;
  time: string;
  activity: string;
}
