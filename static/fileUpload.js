function showUploadWidget() {
    cloudinary.openUploadWidget({
       cloudName: "dmp5wclf8",
       uploadPreset: "HB",
       sources: [
           "url",
           "local"
       ],
       googleApiKey: "<image_search_google_api_key>",
       showAdvancedOptions: true,
       cropping: true,
       multiple: false,
       defaultSource: "local",
       styles: {
           palette: {
               window: "#ffffff",
               sourceBg: "#f4f4f5",
               windowBorder: "#8496AB",
               tabIcon: "#000000",
               inactiveTabIcon: "#555a5f",
               menuIcons: "#555a5f",
               link: "#0433ff",
               action: "#339933",
               inProgress: "#0433ff",
               complete: "#339933",
               error: "#cc0000",
               textDark: "#000000",
               textLight: "#fcfffd"
           },
           fonts: {
               default: null,
               "sans-serif": {
                   url: null,
                   active: true
               }
           }
       }
   },
    (err, info) => {
      if (!err) {    
        console.log("Upload Widget event - ", info);
      }
     });
    }