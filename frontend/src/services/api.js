
const API_BASE_URL = "http://127.0.0.1:8000";


export async function runAutoDS(file) {

  const formData = new FormData();

  formData.append("file", file);


  const response = await fetch(
    `${API_BASE_URL}/api/autods/run`,
    {
      method: "POST",
      body: formData,
    }
  );


  if (!response.ok) {

    let message = "AutoDS pipeline failed.";

    try {

      const errorData = await response.json();

      message =
        errorData.detail ||
        errorData.message ||
        message;

    } catch {

      // Ignore JSON parsing errors

    }

    throw new Error(message);
  }


  return await response.json();
}


export async function checkBackend() {

  const response = await fetch(
    `${API_BASE_URL}/`
  );

  if (!response.ok) {

    throw new Error(
      "Backend server is not responding."
    );

  }

  return await response.json();
}
export const getReportUrl = () => {
  return "http://127.0.0.1:8000/reports/autods_final_report.txt";
};
export const getReportDownloadUrl = () =>
  `${API_BASE_URL}/api/report/download`;