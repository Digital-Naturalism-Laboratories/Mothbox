import fiftyone as fo

#dataset = fo.load_dataset(...)

if __name__ == "__main__":
    # Ensures that the App processes are safely launched on Windows
    #session = fo.launch_app(dataset)
    
    session = fo.launch_app()
    session.wait()