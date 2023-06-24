import os
import Ki67_counter
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile

app = FastAPI()
origins = ['http://localhost:5174']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


myobj = Ki67_counter.initialize_runtime(['-nojvm', '-nodisplay'])
myobj = Ki67_counter.initialize()


@app.post("/count-cell")
async def test(image_file: UploadFile, threshold: float = 0.56):
    try:
        contents = await image_file.read()
        # Create a NamedTemporaryFile to hold the image as a physical file on disk
        temp_file = NamedTemporaryFile(mode="wb", delete=False)
        # Write the contents of the uploaded file to the temporary file
        temp_file.write(contents)
        temp_file.flush()
        # Call the Ki67_counter function with the temporary file path and threshold
        result = myobj.Ki67_counter(temp_file.name, threshold)
        # Close and remove the temporary file
        temp_file.close()
        # temp_file.unlink(missing_ok=True)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Failed to process the image file.")

app.mount('/', StaticFiles(directory='./frontend/dist', html=True))
