import { HttpClientTestingModule, HttpTestingController  } from '@angular/common/http/testing';

import { TestBed } from '@angular/core/testing';
import { HttpClient, HttpResponse, HttpErrorResponse  } from '@angular/common/http';
import { SlogDataService } from './slog-data.service';

describe('SlogDataService', () => {
  //let httpClient: HttpClient;
  //let httpTestingController: HttpTestingController;
  let service: SlogDataService;

  beforeEach(async() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      // providers:[SlogDataService]
    });
    service = TestBed.inject(SlogDataService);
    //httpClient = TestBed.inject(HttpClient);
    //httpTestingController = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
