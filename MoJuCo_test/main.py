from mujoco_py import load_model_from_path, MjSim

model = load_model_from_path("xmls/tosser.xml")

sim = MjSim(model)
sim.step()
print(sim.data.qpos)