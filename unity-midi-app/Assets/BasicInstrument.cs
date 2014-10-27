using UnityEngine;
using System.Collections;

public class BasicInstrument : MonoBehaviour, IInstrument {

	public string iName;
	private AudioSource source;

	void Start () {
		source = (AudioSource) transform.GetComponent("AudioSource");
		Midi.register (this);
	}

	public string getName () {
		return iName;
	}

	public bool playNote (Vector2 pitch) {
		int octave = (int)((pitch.x - 4) * 12);
		source.pitch = Mathf.Pow(2, (octave + pitch.y)/12.0f);
		source.Play();
		return true;
	}
}
