import { Component } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.css'
})
export class UploadComponent {
  constructor(private http: HttpClient) {}
  selectedFile: File | null = null;
  uploadUrlEndpoint = 'http://127.0.0.1:8000/upload/'; 
  message = 'Upload a PDF file'

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    if (this.selectedFile != null) {
      this.uploadPDF(this.selectedFile)
      this.message = 'File succesfully uploaded'
    }
  }

  uploadPDF(file: File) {
    const formData = new FormData();
    formData.append('pdf_file', file);
    this.http.post(this.uploadUrlEndpoint, formData)
      .subscribe(response => {
        console.log(response);
      }, (error: HttpErrorResponse) => {
        console.error('Error uploading file', error);
      });
  }
}
