using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Conveyor : MonoBehaviour
{
    public float speed = 1f;
    public float visualSpeedScalar = 1f;

    private float currentScroll;
    public bool hasIncomingCargo = false;
    public bool hasStationaryCargo = false;
    public Conveyor nextInPath;
    public int storageCapacity = 1;
    public int itemsStored = 0;

    Vector3 top;
    Vector3 inFront;

    private void Start()
    {
        top = transform.position;
        inFront = transform.forward + transform.position;
        SetNextInPath();
    }

    private void SetNextInPath()
    {
        Collider[] hitColliders = Physics.OverlapSphere(inFront, 0.1f);
        foreach (var hitCollider in hitColliders)
        {
            Conveyor otherConveyor = hitCollider.GetComponent<Conveyor>();
            if (otherConveyor == null)
                continue;
            nextInPath = otherConveyor;
            return;
        }
    }

    private void Update()
    {
        ScrollTexture();
    } 
    
    public bool OutputClear()
    {
        if (nextInPath != null && nextClear())
        {
            return true;
        }
        
        return false;
    }

    private bool nextClear()
    {
        return !nextInPath.hasIncomingCargo && !nextInPath.hasStationaryCargo && itemsStored < storageCapacity;
    }

    public Vector3 GetTargetPos()
    {
        return inFront;
    }
    
    void ScrollTexture()
    {
        currentScroll = currentScroll + Time.deltaTime * speed * visualSpeedScalar;
        GetComponent<Renderer>().material.mainTextureOffset = new Vector2(0, currentScroll);
    }

    
}
