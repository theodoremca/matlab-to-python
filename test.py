import Ki67_counter
image = './for_testing/Picture1.png'



myobj = Ki67_counter.initialize_runtime(['-nojvm', '-nodisplay'])
myobj = Ki67_counter.initialize()
print(myobj.Ki67_counter(image, 0.56))