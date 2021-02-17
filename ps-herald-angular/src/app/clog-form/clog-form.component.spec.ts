import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { HttpClient, HttpResponse, HttpErrorResponse } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { ClogFormComponent } from './clog-form.component';
import { FormsModule } from '@angular/forms';
import { SlogDataService } from '../slog-data.service'
//import { HttpClientModule } from '@angular/common/http';
//import { HttpClient} from '@angular/common/http';
//import { HttpClientTestingModule} from '@angular/common/http/testing';

describe('ClogFormComponent', () => {
  let httpClient: HttpClient;
  let component: ClogFormComponent;
  let fixture: ComponentFixture<ClogFormComponent>;
  let element;
  let service;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports:[FormsModule],
      declarations: [ ClogFormComponent ],
      providers: [SlogDataService ]
    })
    .compileComponents();
  });

  //beforeEach(() => { slogdataService = new SlogDataService(); });
  beforeEach(() => {
    fixture = TestBed.createComponent(ClogFormComponent);
    component = fixture.componentInstance; // to access properties and methods
    element = fixture.nativeElement;  // to access DOM element 
    component.ngOnInit();
    fixture.detectChanges();
    service = TestBed.inject(SlogDataService); 
    httpClient = TestBed.inject(HttpClient);
  });

//  it('should create', () => {
//    expect(component).toBeTruthy();
//  });
//  it('submitted should be initialized and updated on submit', () => {
//    expect(component.submitted).toBe(false,"false is initial Value");
//    component.onSubmit();
//    expect(component.submitted).toBe(true,"false is initial Value");
//  });
//  it('Search_values should be initialized ', () => {
//    expect(component.submitted).toBe(false,"false is initial Value");
//    expect(component.search_tuple.system_id).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.system_id).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.sub_system_id).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.sub_sub_system_id).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.user_spec1).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.user_spec2).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.produkt_id).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.pattern).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.starting_at).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.notify_level).toBe("10)","is initial Value");
//    expect(component.search_tuple.num_records).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.max_rows).toBe("not_selected","is initial Value");
//    expect(component.search_tuple.order).toBe("desc","is initial Value");
//  });
//  
});
